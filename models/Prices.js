const mongoose = require('mongoose');

const pricesSchema = new mongoose.Schema({
  name: String
});

const Prices = mongoose.model('Prices', pricesSchema);
module.exports = Prices;
