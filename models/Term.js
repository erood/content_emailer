const mongoose = require('mongoose');

const termSchema = new mongoose.Schema({
  name: String
});

const Term = mongoose.model('Term', termSchema);
module.exports = Term;