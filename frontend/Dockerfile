FROM node:20-alpine

WORKDIR /app

COPY . .

RUN npm install && npm install react-router-dom

CMD ["npm", "run", "dev"]