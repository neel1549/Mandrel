# Base image
FROM node:17

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

# Install the 'serve' package to avoid runtime installation
RUN npm install -g serve

COPY . .

RUN npm run build

EXPOSE 5173

# Default to 3000 if not specified by Heroku
CMD ["sh", "-c", "npx serve -s dist -l ${PORT:-3000}"]