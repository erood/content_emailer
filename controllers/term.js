/**
 * GET /terms
 * List all terms.
 */
const Term = require('../models/Term.js');

exports.getTerms = (req, res) => {
  Term.find((err, docs) => {
    res.render('terms', { terms: docs });
  });
};