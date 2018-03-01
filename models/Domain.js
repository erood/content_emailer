const mongoose = require('mongoose');

const domainSchema = new mongoose.Schema({
  domain: String,
  submissions: String,
  score: Number,
  subreddit: String,
  avg_score: Number,
  total_upvotes: Number,
  classify: String


}, { timestamps: true });

const Domain = mongoose.model('Domain', domainSchema);
module.exports = Domain;
