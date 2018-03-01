/**
 * GET /blog
 * List all blog.
 */
const Blog = require('../models/Blog.js');

exports.getBlog = (req, res) => {
  Blog.find((err, docs) => {
    res.render('blog', { blog: docs });
  });
};