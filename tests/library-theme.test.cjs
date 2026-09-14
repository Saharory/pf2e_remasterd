const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const root = path.resolve(__dirname, '..');
const stylesheet = fs.readFileSync(path.join(root, 'styles', 'default.css'), 'utf8');

test('library footer tags keep readable colors in light and dark modes', () => {
  assert.match(stylesheet, /--footer-tag-background:\s*white;/);
  assert.match(stylesheet, /--pf-dark-tag:\s*#302d2b;/);
  assert.match(stylesheet, /--pf-dark-tag-text:\s*#ddd6cc;/);
  assert.match(stylesheet, /--footer-tag-background:\s*var\(--pf-dark-tag\);/);
  assert.match(stylesheet, /--footer-tag-text:\s*var\(--pf-dark-tag-text\);/);
  assert.match(stylesheet, /background-color:\s*var\(--footer-tag-background\);/);
  assert.match(stylesheet, /color:\s*var\(--footer-tag-text\);/);
});
