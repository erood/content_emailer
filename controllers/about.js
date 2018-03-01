/**
 * GET /about_page
 * List all about_page.
 */
const About = require('../models/About.js');

exports.getAbouts = (req, res) => {
  About.find((err, docs) => {
    res.render('about_page', { about_page: docs });
  });
};
