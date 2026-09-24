import assert from "node:assert/strict";
import { createHash, webcrypto } from "node:crypto";
import { readFile } from "node:fs/promises";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import vm from "node:vm";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const readJson = async (file) => JSON.parse(await readFile(path.join(root, file), "utf8"));
const manifest = await readJson("public-manifest.json");
const siteBaseUrl = manifest.build.siteBaseUrl;
const sitePath = new URL(siteBaseUrl + "/").pathname;

async function joinStatus(cardPath) {
  const cardBytes = await readFile(path.join(root, cardPath));
  const envelope = {
    card: `${siteBaseUrl}/${cardPath}`,
    sha256: createHash("sha256").update(cardBytes).digest("hex"),
    v: 1
  };
  const location = new URL(`${siteBaseUrl}/hub/join/`);
  location.hash = "#v1." + Buffer.from(JSON.stringify(envelope)).toString("base64url");
  const elements = new Map([
    "status", "failure", "machine-readable", "machine-section", "verified-title",
    "summary", "steps", "repository-link", "json-link", "llms-link", "verified"
  ].map((id) => [id, {
    hidden: true, textContent: "", children: [], append(item) { this.children.push(item); }
  }]));
  let finish;
  const completed = new Promise((resolve) => { finish = resolve; });
  Object.defineProperty(elements.get("status"), "textContent", {
    set(value) {
      this.value = value;
      if (value.startsWith("Verification complete.") || value === "Verification failed.") finish(value);
    },
    get() { return this.value || ""; }
  });
  vm.runInNewContext(await readFile(path.join(root, "hub/join/join.js"), "utf8"), {
    TextDecoder, TextEncoder, URL, URLSearchParams, Uint8Array, atob, btoa,
    document: { getElementById: (id) => elements.get(id), createElement: () => ({ textContent: "" }) },
    fetch: async (url) => {
      const parsed = new URL(url);
      assert.ok(parsed.pathname.startsWith(sitePath));
      const bytes = await readFile(path.join(root, parsed.pathname.slice(sitePath.length)));
      return {
        ok: true,
        arrayBuffer: async () => bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength)
      };
    },
    window: { atob, btoa, crypto: webcrypto, history: { replaceState() {} }, location }
  });
  let timer;
  const status = await Promise.race([
    completed,
    new Promise((_, reject) => { timer = setTimeout(() => reject(new Error("join timed out")), 5000); })
  ]);
  clearTimeout(timer);
  return { status, failure: elements.get("failure").textContent, machine: elements.get("machine-readable").textContent };
}

test("every predecessor join card still verifies end to end on the published join page", async () => {
  const pins = await readJson("seed-src/SEED_PREDECESSORS.json");
  const index = await readJson("api/hive-hub/v1/organization-seeds.json");
  const dialbook = await readJson("api/hive-hub/v1/dialbook.json");
  const active = new Set(dialbook.records.map((descriptor) => descriptor.path));
  assert.equal(Object.keys(pins.seeds).length, 12);
  for (const [slug, history] of Object.entries(pins.seeds)) {
    const earlier = history.at(-1);
    const current = index.seeds.find((seed) => seed.slug === slug);
    assert.deepEqual(current.predecessors.map((item) => item.card.path), [earlier.card.path]);
    assert.ok(!active.has(earlier.record.path), `${slug}: a predecessor entered the active dialbook`);
    const result = await joinStatus(earlier.card.path);
    assert.match(result.status, /^Verification complete/, `${slug}: ${result.failure}`);
    const verified = JSON.parse(result.machine);
    assert.equal(verified.seed.archive.sha256, earlier.archive.sha256);
    assert.notEqual(verified.seed.archive.sha256, current.archive.sha256);
  }
});

test("the site says where every starter fits and shows its folder-Hive template", async () => {
  const home = await readFile(path.join(root, "hub/index.html"), "utf8");
  assert.match(home, /id="where-this-fits"/);
  assert.match(home, /discovery and join across Hives/);
  assert.match(home, /Transport carries; signatures decide\./);
  const llms = await readFile(path.join(root, "llms.txt"), "utf8");
  assert.match(llms, /\n## Where this fits\n/);
  assert.match(llms, /rapp-hive\/2 is frozen as a research record/);
  const index = await readJson("api/hive-hub/v1/organization-seeds.json");
  for (const seed of index.seeds) {
    const page = await readFile(path.join(root, "hub/seeds", seed.slug, "index.html"), "utf8");
    assert.match(page, /A starter package, not an activated organization\./);
    for (const word of ["[in force]", "[specified]", "[candidate]"]) assert.ok(page.includes(word), `${seed.slug}: ${word}`);
    assert.ok(page.includes("folder-hive/\n├── .gitattributes\n├── HIVE.md\n└── shared/"), seed.slug);
    assert.match(page, /Earlier package, kept byte for byte\./);
    assert.equal(seed.folderHive.hive, null);
    assert.equal(seed.folderHive.health, "experimental");
  }
});
