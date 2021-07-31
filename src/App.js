import { useEffect, useState } from 'react';
import script from './python/script.py';
import logo from './logo.svg';
import './App.css';

const App = () => {
  const [runScript, setRunScript] = useState(false);
  const [output, setOutput] = useState('(loading...)');

  const [pythonFile, setPythonFile] = useState(null);
  const [loadedNumpy, setLoadedNumpy] = useState(false);

  useEffect(() => {
    if (!pythonFile || !loadedNumpy) {
      window.languagePluginLoader.then(() => {
        fetch(script)
          .then((src) => src.text())
          .then((code) => setPythonFile(code))
          .then(() =>
            window.pyodide
              .loadPackage(['numpy'])
              .then(() => setLoadedNumpy(true))
          );
      });
    }
  }, [loadedNumpy, pythonFile]);

  useEffect(() => {
    // Once python script and numpy have been loaded
    if (pythonFile && loadedNumpy) {
      let my_js_namespace = { x: 3 };
      window.pyodide.registerJsModule('my_js_namespace', my_js_namespace);
      const output = window.pyodide.runPython(pythonFile);
      const testFunc = window.pyodide.globals.get('testFunc');
      console.log(testFunc());
      // console.log(my_js_namespace.y);
    }
  }, [pythonFile, loadedNumpy]);

  const runPyScript = (code) => {
    window.pyodide.loadPackage(['numpy']).then(() => {
      const output = window.pyodide.runPython(code);
      setOutput(output);
    });
  };

  useEffect(() => {
    if (runScript) {
      window.languagePluginLoader.then(() => {
        fetch(script)
          .then((src) => src.text())
          .then(runPyScript);
      });
    }
  }, [runScript]);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>{output}</p>
        <button onClick={() => setRunScript((prevRunScript) => !prevRunScript)}>
          Run script
        </button>
      </header>
    </div>
  );
};

export default App;
