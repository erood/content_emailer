const mongoose = require('mongoose');

const recordSchema = new mongoose.Schema({
  name: String,
  website: String,
  description: String,
  audience: String,
  open_rate: String,
  ctr: String,
  pricing: String,
  contact_method: String,
  email: String,
  content_type: String

}, { timestamps: true });

const Record = mongoose.model('Record', recordSchema);
module.exports = Record;
