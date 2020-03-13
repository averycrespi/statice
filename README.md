<h1 align="center">
    <br>
    <img src="https://raw.githubusercontent.com/averycrespi/statice/master/resources/logo.png" width="150"</img>
    <br>
    Statice
    <br>
</h1>

<h4 align="center">A friendly status page.</h4>

<p align="center">
    <a href="#features">Features</a> •
    <a href="#getting-started">Getting Started</a> •
    <a href="#credits">Credits</a> •
    <a href="#license">License</a>
</p>

<p align="center">
    <img src="https://raw.githubusercontent.com/averycrespi/statice/master/resources/screenshot.png" width="600"/>
</p>

## Features

- Create checks to watch your pages
- Monitor HTTP status codes and response times
- Easily tweak performance with environment variables

## Getting Started

Requirements:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

```sh
# Clone the repository.
git clone git@github.com:averycrespi/statice.git && cd statice

# Set environment variables (optional).
cp .env.example .env

# Build and start containers.
docker-compose up -d
```

## Development

Requirements:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Make](https://www.gnu.org/software/make/)
- [Poetry](https://python-poetry.org/)
- [Python](https://www.python.org/) (3.6 or newer)

```sh
# Clone the repository.
git clone git@github.com:averycrespi/statice.git && cd statice

# Enable Docker Compose overrides.
cp docker-compose.override.yml.example docker-compose.override.yml

# Configure the environment for development.
make dev
```

## Credits

- Built with [Flask](https://www.palletsprojects.com/p/flask/) and [Bootstrap](https://getbootstrap.com/)
- Styled with the Flatly theme from [Bootswatch](https://bootswatch.com/)
- Logo derived from: flowers by ruliani2018 from the [Noun Project](https://thenounproject.com)

## License

[MIT](https://choosealicense.com/licenses/mit/)
