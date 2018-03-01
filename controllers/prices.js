/**
 * GET /books
 * List all books.
 */

 
const Prices = require('../models/Prices.js');

exports.getPrices = (req, res) => {
  Prices.find((err, docs) => {
    res.render('prices', { prices: docs });
  });
};
