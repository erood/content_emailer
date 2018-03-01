/**
 * GET /weights
 * List all weights.
 */
const Weight = require('../models/Weight.js');

exports.getWeights = (req, res) => {
  Weight.find((err, docs) => {
    res.render('weights', { weights: docs });
  });
};

/**
 * POST /weights
 * Skeleton for now.
 */
exports.postWeights = (req, res) => {
  Weight.find((err, docs) => {
    res.render('weights', { weights: docs });
  });
};
