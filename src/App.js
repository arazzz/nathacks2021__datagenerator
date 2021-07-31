import { useEffect, useState, useCallback } from 'react';
import script from './python/script.py';
import logo from './logo.svg';
import './App.css';
import Chart from 'react-apexcharts';

const App = () => {
  const [loadData, setLoadData] = useState(false);
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

  const [data, setData] = useState([]);

  const visualizeData = useCallback(() => {
    // Once python script and numpy have been loaded
    if (pythonFile && loadedNumpy) {
      const output = window.pyodide.runPython(pythonFile);
      const generate_data = window.pyodide.globals.get('generate_data');
      setData(generate_data().toJs());

      return () => {
        output.destroy();
        generate_data.destroy();
      };
    }
  }, [pythonFile, loadedNumpy]);

  const chartData = {
    options: {
      chart: {
        id: 'data',
      },
      xaxis: {
        type: 'numeric',
      },
    },
    series: [
      {
        name: 'series-1',
        data: data,
      },
    ],
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        {/* <p>{output}</p> */}
        <Chart
          options={chartData.options}
          series={chartData.series}
          type="line"
          width="500"
        />
        <button onClick={() => visualizeData()}>Load data</button>
      </header>
    </div>
  );
};

export default App;
