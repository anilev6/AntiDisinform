# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Install Poetry for Python package management
RUN pip install poetry

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the pyproject.toml file into the container
COPY pyproject.toml /usr/src/app/

# Install dependencies using poetry in a way that doesn't create a virtual environment
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy the rest of the application's code
COPY . .

# (Optional) expose the port the app runs on
# EXPOSE 80

# Build the package
RUN poetry build

# Install the package itself
RUN poetry install

# # # Set the default command to be run in the container
# CMD ["poetry", "run", "python", "frontend/main.py"]
# Set the default command to launch the CLI
ENTRYPOINT ["python", "frontend/main.py"]
