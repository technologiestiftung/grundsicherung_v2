Second version of Grundsicherung website 

**New Features are**
* ES6 Support via [babel](https://babeljs.io/) (v7)
* SASS Support via [sass-loader](https://github.com/jtangelder/sass-loader)
* Linting via [eslint-loader](https://github.com/MoOx/eslint-loader)

### Installation

```
nvm use 13
npm install
```

### Start Dev Server
  
```
npm start
```

### Build Prod Version

```
npm run build
```

When you run `npm run build` we use the [mini-css-extract-plugin](https://github.com/webpack-contrib/mini-css-extract-plugin) to move the css to a separate file. The css file gets included in the head of the `index.html`.

### For realtime development
change path in timelapse.js and map.js from 
```
d3.json("config.json")
```
to
```
d3.json("src/config.json")
```
