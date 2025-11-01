import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import archiver from 'archiver';

/**
 * Creates a ZIP file of the Chrome extension
 * Run this script to package the extension for distribution
 */

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const EXTENSION_DIR = path.join(__dirname, '..', 'chrome-extension');
const OUTPUT_DIR = path.join(__dirname, '..', 'public');
const OUTPUT_FILE = path.join(OUTPUT_DIR, 'verify-extension.zip');

// Ensure output directory exists
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Create a file to stream archive data to
const output = fs.createWriteStream(OUTPUT_FILE);
const archive = archiver('zip', {
  zlib: { level: 9 } // Maximum compression
});

// Listen for all archive data to be written
output.on('close', () => {
  console.log('✅ Extension packaged successfully!');
  console.log(`📦 File: ${OUTPUT_FILE}`);
  console.log(`📊 Size: ${(archive.pointer() / 1024 / 1024).toFixed(2)} MB`);
  console.log('\n🎉 Ready for distribution!');
  console.log('📍 Users can download from: /verify-extension.zip');
});

// Handle warnings
archive.on('warning', (err) => {
  if (err.code === 'ENOENT') {
    console.warn('⚠️ Warning:', err);
  } else {
    throw err;
  }
});

// Handle errors
archive.on('error', (err) => {
  throw err;
});

// Pipe archive data to the file
archive.pipe(output);

console.log('📦 Packaging Chrome extension...\n');

// Add the chrome-extension directory to the archive
archive.directory(EXTENSION_DIR, 'chrome-extension');

// Finalize the archive
archive.finalize();
