const { spawn } = require('child_process');

module.exports = (image, answerKeys) => {
  const pythonProcess = spawn('python3', [
    './scripts/omr.py',
    image,
    answerKeys,
  ]);

  pythonProcess.stdout.on('data', (data) => {
    console.log(data.toString());
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data.toString()}`);
  });
};
