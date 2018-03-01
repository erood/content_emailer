/**
 * GET /reddit_creators
 * List all reddit_creators.
 */
const Reddit_Creator = require('../models/Reddit_Creator.js');

exports.getReddit_Creators = (req, res) => {
  Reddit_Creator.find((err, docs) => {
    res.render('reddit_creators', { reddit_creators: docs });
  });
};