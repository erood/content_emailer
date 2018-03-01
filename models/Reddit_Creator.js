const mongoose = require('mongoose');

const reddit_creatorSchema = new mongoose.Schema({
  name: String
});

const Reddit_Creator = mongoose.model('Reddit_Creator', reddit_creatorSchema);
module.exports = Reddit_Creator;