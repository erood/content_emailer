const mongoose = require('mongoose');

const domainSchema = new mongoose.Schema({
  
  domain: String,
  subreddit: String,
  classify: String,
  median_score: Number,
  submissions: String,
  avg_score: Number,
  total_upvotes: Number,
  update_date: Date
  

}, { timestamps: true });

const Domain = mongoose.model('Domain', domainSchema);
module.exports = Domain;
