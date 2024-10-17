const express = require('express');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(express.static('public'));
app.use(express.json());

// Serve HTML pages
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/menu.html'));
});

app.get('/game', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/game.html'));
});

// Generate statistics and then serve the result page
app.get('/result', (req, res) => {
  // First, generate statistics before serving result.html
  exec('python scripts/statistic.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error.message}`);
      return res.status(500).send('Error generating statistics');
    }
    if (stderr) {
      console.error(`Python stderr: ${stderr}`);
      return res.status(500).send('Error in Python script');
    }

    // After generating statistics, serve the result page
    res.sendFile(path.join(__dirname, 'public/result.html'));
  });
});

// Fetch a random sentence
app.get('/get-sentence', (req, res) => {
  exec(`python scripts/data_processor.py get_sentence`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error.message}`);
      return res.status(500).send('Error fetching sentence');
    }
    if (stderr) {
      console.error(`Python stderr: ${stderr}`);
      return res.status(500).send('Error in Python script');
    }

    try {
      const result = JSON.parse(stdout);
      res.json({ sentence: result.sentence });
    } catch (parseError) {
      console.error('Error parsing JSON:', parseError);
      res.status(500).send('Error parsing sentence data');
    }
  });
});

// Save input history (always overwrite the file)
app.post('/save-input-history', (req, res) => {
  const { history, difficulty, score, level } = req.body;
  const logFilePath = path.join(__dirname, 'input_history.json');

  // Prepare the new log entry
  const logEntry = {
    timestamp: new Date().toISOString(),
    difficulty,
    score,
    level,
    history
  };

  // Overwrite the file with the new log entry (removes any previous data)
  fs.writeFile(logFilePath, JSON.stringify([logEntry], null, 2), (err) => {
    if (err) {
      console.error('Error saving input history:', err);
      return res.status(500).send('Error saving input history');
    }
    res.status(200).send('Input history saved successfully');
  });
});

// Save game data (JSON formatted)
app.post('/save-game-data', (req, res) => {
  const gameData = req.body;
  const logFilePath = path.join(__dirname, 'input_history.json');
  console.log(`saving`);
  fs.writeFile(logFilePath, JSON.stringify(gameData, null, 2), (err) => {
    if (err) {
      console.error('Error saving game data:', err);
      return res.status(500).send('Error saving game data');
    }
    res.status(200).send('Game data saved successfully');
  });
});

// Generate statistics
app.get('/generate-statistics', (req, res) => {
 
  exec('python3 scripts/statistic.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error.message}`);
      return res.status(500).send('Error generating statistics');
    }
    if (stderr) {
      console.error(`Python stderr: ${stderr}`);
      return res.status(500).send('Error in Python script');
    }

    console.log('Statistics generated successfully');
    res.status(200).send('Statistics generated successfully');
  });
});

// Serve static files in the output directory
app.use('/output', express.static(path.join(__dirname, 'output')));

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
