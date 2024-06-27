# Site
+---------------------+      +-------------------+      +-----------------+
|                     |      |                   |      |                 |
|     Frontend        |      |    Backend        |      |   Database      |
|     (React)         +----->|    (Flask)        +----->|   (MongoDB)     |
|                     |      |                   |      |                 |
+----------+----------+      +--------+----------+      +--------+--------+
           |                          |                          ^
           |                          |                          |
           |                          v                          |
           |               +----------+----------+               |
           |               |                     |               |
           |               |     Computer        |               |
           +-------------->|     Vision (OpenCV) |               |
                           |                     |               |
                           +----------+----------+               |
                                      |                          |
                                      v                          |
                           +----------+----------+               |
                           |                     |               |
                           |     MyCobot Robot   |<--------------+
                           |                     |
                           +---------------------+

## Frontend (React)

Users upload an image via the web interface.
The image is sent to the Flask backend through an API request.

## Backend (Flask)

Receives the image from the frontend.
Uses OpenCV to process the image.
Stores the processed image metadata or any other relevant data in MongoDB.
Sends the image or instructions to the MyCobot robot.

## Database (MongoDB)

Stores image data and metadata.
Keeps records of the processed images and any associated data.

## MyCobot Robot (Other repositore)

Receives instructions from the Flask backend.
Processes the instructions to reproduce the painting on a canvas.

