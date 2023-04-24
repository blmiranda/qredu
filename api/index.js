const express = require('express');
const scanImage = require('./functions/scanImage');

const app = express();
const PORT = 3000;

app.use(express.json({ limit: '10mb' }));

app.post('/', (req, res) => {
  const { image, answerKeys } = req.body;

  if (!image || !answerKeys) {
    return res
      .status(418)
      .send({ message: 'we need the image and the answerKeys' });
  }

  scanImage(image, JSON.stringify(answerKeys));

  res.send({
    result: '100%',
  });
});

app.listen(PORT, () => {
  console.log(`Listening on http://localhost:${PORT}`);
});
