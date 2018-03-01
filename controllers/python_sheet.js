/**
 * GET /python_sheets
 * List all python_sheets.
 */
const Python_Sheet = require('../models/Python_Sheet.js');

exports.getPython_Sheets = (req, res) => {
  Python_Sheet.find((err, docs) => {
    res.render('python_sheets', { python_sheets: docs });
  });
};