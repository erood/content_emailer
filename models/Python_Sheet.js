const mongoose = require('mongoose');

const python_sheetSchema = new mongoose.Schema({
  name: String
});

const Python_Sheet = mongoose.model('Python_Sheet', python_sheetSchema);
module.exports = Python_Sheet;