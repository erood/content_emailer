const mongoose = require('mongoose');

const logbookSchema = new mongoose.Schema({
  name: String
});

const Logbook = mongoose.model('Logbook', logbookSchema);
module.exports = Logbook;
