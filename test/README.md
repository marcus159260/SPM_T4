# Test cases

## Frontend JavaScript tests - Jest

I'm using Jest for my JavaScript tests
https://jestjs.io/docs/getting-started

### Jest installation
1. Under root dir, install Jest and the Babel stuff:
```sh
npm install --save-dev jest @babel/preset-env @babel/register @babel/core babel-jest 
```

### Jest steps
1. Under test folder, create test file '{name}.test.js'
2. Ensure that your functions can be imported into your test.js
   - Example: You are testing demo() that is only locally available in your Demo.vue, try to place your demo() in a separate js folder under frontend/src/util -> import into your Demo.vue & test.js [check the existing periodPolicy.js]. Or you can try mounting the Vue component and using the function directly (?) -- chatGPT this.
4. To run a particular test file (replace this with your test file):
```sh
cd test npm test demo.test.js
```
3. To run all the test files:
```sh
npm test
```
