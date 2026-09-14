const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const root = path.resolve(__dirname, '..');
const stylesheet = fs.readFileSync(path.join(root, 'styles', 'default.css'), 'utf8');

test('library footer tags keep readable colors in light and dark modes', () => {
  assert.match(stylesheet, /--footer-tag-background:\s*white;/);
  assert.match(stylesheet, /--footer-tag-background:\s*#26332a;/);
  assert.match(stylesheet, /--footer-tag-text:\s*#cbd2cc;/);
  assert.match(stylesheet, /background-color:\s*var\(--footer-tag-background\);/);
  assert.match(stylesheet, /color:\s*var\(--footer-tag-text\);/);
});
