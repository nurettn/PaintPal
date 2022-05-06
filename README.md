# PaintPal
![PaintPal](https://github.com/nurettinabaci/PaintPal/blob/master/paint_pal.png)

> Draw and guess the words game. Create your own room and play with your friends.




## Run the project locally
1. Open the command line and clone the project to your local
```bash
git clone https://github.com/nurettinabaci/PaintPal.git
```

2. Go to project folder and create a Docker image
```bash
docker build --tag drawing.game:latest .
```

3. Run a container from image

```bash
docker run --publish 8000:8000 --detach --name paintpal drawing.game:latest
```

```bash
docker-compose up
```

You're ready to go!



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Don't forget to update `requirements.txt` file.

## License
MIT License
