const mongoose = require('mongoose');

const goalSchema = new mongoose.Schema({
  name: String,
  email: String,
  goal_start: String,
  enter_goals: String,
  goal_weight: Number,
  start_weight: Number,
  goal_date: String,
  weight_units: String,


}, { timestamps: true });

const Goal = mongoose.model('Goal', goalSchema);
module.exports = Goal;
