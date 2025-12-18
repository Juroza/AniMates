# AniMates

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

### General Development Workflow

#### When working on Frontend

##### Start Express Server

The thing that starts the sockets and what not, need this started to call backend from frontend buttons and things

```sh
npm start
```

For local backend to work ur gonna need to also run

```sh
cd backend
func start
```

##### Start Frontend Environment

```sh
cd frontend
npm install
npm run dev
```

### When working on Backend

```sh
cd backend
pip install -r requirements.txt
func start
```

## When your finished with what ur working on

### Best Practice

Any git push to main branch will automatically reflect on the [published site](https://animates-fkaudbd3ejhmcwdp.francecentral-01.azurewebsites.net/). Its probably best to have at least someone else check it first

#### Best Practice

```sh
git pull
git checkout -b [your_feature]
```

When done

```sh
git add .
git commit
git push
```

#### If cba just

```sh
git add .
git commit
git push
```

directly on the main branch

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
