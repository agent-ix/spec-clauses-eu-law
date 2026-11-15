#!/usr/bin/env node
// Stage module resources at the npm package root during `npm pack`.
import {
  cpSync,
  existsSync,
  mkdirSync,
  readFileSync,
  renameSync,
  rmdirSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const moduleDir = "spec_clauses_eu_law";
const resources = ["manifest.yaml", "clauses"];
const backupRoot = join(root, ".npm-stage-backup");
const ownershipFile = join(backupRoot, "owned.json");

function clean() {
  if (!existsSync(backupRoot)) return;
  if (!existsSync(ownershipFile)) {
    try {
      rmdirSync(backupRoot);
      return;
    } catch (error) {
      if (error.code === "ENOTEMPTY" || error.code === "EEXIST") {
        throw new Error("stage-npm: refusing to remove an unowned backup directory");
      }
      throw error;
    }
  }

  const { originals } = JSON.parse(readFileSync(ownershipFile, "utf8"));
  for (const resource of resources) {
    const backup = join(backupRoot, resource);
    const target = join(root, resource);
    if (existsSync(backup)) {
      rmSync(target, { recursive: true, force: true });
      renameSync(backup, target);
    } else if (!originals.includes(resource)) {
      rmSync(target, { recursive: true, force: true });
    }
  }
  rmSync(backupRoot, { recursive: true, force: true });
}

if (process.argv.includes("--clean")) {
  clean();
} else {
  if (existsSync(backupRoot)) {
    if (existsSync(ownershipFile)) {
      throw new Error("stage-npm: unfinished staging backup exists; run --clean");
    }
    try {
      rmdirSync(backupRoot);
    } catch (error) {
      if (error.code === "ENOTEMPTY" || error.code === "EEXIST") {
        throw new Error("stage-npm: refusing to remove an unowned backup directory");
      }
      throw error;
    }
  }
  const sourceRoot = join(root, moduleDir);
  if (!existsSync(sourceRoot)) throw new Error(`stage-npm: missing ${moduleDir}`);
  mkdirSync(backupRoot);
  const originals = resources.filter((resource) => existsSync(join(root, resource)));
  writeFileSync(ownershipFile, JSON.stringify({ version: 1, originals }));
  try {
    for (const resource of resources) {
      const destination = join(root, resource);
      if (existsSync(destination)) renameSync(destination, join(backupRoot, resource));
      const source = join(sourceRoot, resource);
      if (existsSync(source)) cpSync(source, destination, { recursive: true });
    }
  } catch (error) {
    clean();
    throw error;
  }
}
