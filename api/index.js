const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());

app.post('/', (req, res) => {
  const { image } = req.body;

  console.log(req.body);

  if (!image) {
    res.status(418).send({ message: 'we need an image' });
  }

  res.send({
    result: '100%',
  });
});

app.listen(PORT, () => {
  console.log(`Listening on http://localhost:${PORT}`);
});
