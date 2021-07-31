import React, { useContext, useEffect, useState, useCallback } from 'react';

// Styling
import { Box, Button, Grid, Slider, Typography } from '@material-ui/core';
import styled, { css, keyframes } from 'styled-components';
import { darken, getLuminance, lighten, mix, rgba } from 'polished';
import { motion } from 'framer-motion';
import 'styled-components/macro';

// Helpers
import { docReady, checkVisible } from 'utils/helpers';

// Plotting
import Chart from 'react-apexcharts';

// Helpers
import {
  ClearBlock,
  GridContainer,
  PageContainer,
  SpacedGridContainer,
} from 'components/styles/global';

// Scripts
import script from 'python/script.py';
import useDidMountEffect from 'components/useDidMountEffect';
import { AppContext } from 'contexts/AppContext';

// #region NOTES
/* 
    Using namespaces to pass JS vars to Python
    let my_js_namespace = { x : 3 };
    pyodide.registerJsModule("my_js_namespace", my_js_namespace);
    pyodide.runPython(`
        from my_js_namespace import x
        print(x) # 3
        my_js_namespace.y = 7
    `);
    console.log(my_js_namespace.y); // 7
*/
// #endregion END NOTES

const Loader = styled(
  ({ loaded, children, loader = 'Loading...', ...props }) => {
    const [show, setShow] = useState(false);
    useDidMountEffect(() => {
      setShow(true);
    }, [loaded]);

    return <>{show ? children : loader}</>;
  }
)``;

const IndexPage = styled(({ ...props }) => {
  const appCtx = useContext(AppContext);
  useEffect(() => {
    appCtx.setMainLayoutOptions({
      pageTitle: 'EEG Data Generator',
    });
  }, [appCtx.setMainLayoutOptions]);

  const [pythonFile, setPythonFile] = useState(null);
  const [loadedNumpy, setLoadedNumpy] = useState(false);
  const [data, setData] = useState([]);

  //   Slider vars
  const [tAmp, setTAmp] = useState(0.2);
  const [bAmp, setBAmp] = useState(0.2);
  const [sliderUpdateComplete, setSliderUpdateComplete] = useState(true);
  const [slidersNamespace, setSlidersNamespace] = useState({
    epochDuration: 0.25,
    samplingRate: 512,
    tAmp: tAmp, // 0 - 0.5 mV
    tFreq: 5, // 3.5 - 7
    tNoise: 1, // 0 - 10
    bAmp: bAmp, // 0 - 0.5 mV
    bFreq: 15, // 12 - 20
    bNoise: 1, // 0 - 10
  });

  const [sliderConfigs, setSliderConfigs] = useState({ minAmp: 0, maxAmp: 10 });

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

  const visualizeData = useCallback(() => {
    // Once python script and numpy have been loaded
    if (pythonFile && loadedNumpy) {
      window.pyodide.registerJsModule('sliders_namespace', slidersNamespace);
      const output = window.pyodide.runPython(pythonFile);
      const generate_data = window.pyodide.globals.get('generate_data');
      setData(generate_data(slidersNamespace).toJs());

      return () => {
        output.destroy();
        generate_data.destroy();
      };
    }
  }, [pythonFile, loadedNumpy]);

  useDidMountEffect(() => {
    if (
      pythonFile &&
      loadedNumpy &&
      data &&
      slidersNamespace &&
      !sliderUpdateComplete
    ) {
      //   console.log(slidersNamespace.bAmp, slidersNamespace.tAmp);
      window.pyodide.registerJsModule('sliders_namespace', slidersNamespace);
      const output = window.pyodide.runPython(pythonFile);
      const generate_data = window.pyodide.globals.get('generate_data');
      setData(generate_data(slidersNamespace).toJs());

      setSliderUpdateComplete(true);

      return () => {
        output.destroy();
        generate_data.destroy();
      };
    }
  }, [pythonFile, loadedNumpy, data, slidersNamespace, sliderUpdateComplete]);

  const sliderCB = (value, type) => {
    let sliders_namespace = {
      ...slidersNamespace,
      tAmp: type === 'theta' ? value : slidersNamespace.tAmp, // 0 - 0.5 mV
      bAmp: type === 'beta' ? value : slidersNamespace.bAmp, // 0 - 0.5 mV
    };
    setSlidersNamespace(sliders_namespace);
    setSliderUpdateComplete(false);
  };

  const chartData = {
    options: {
      chart: {
        id: 'data',
      },
      xaxis: {
        type: 'numeric',
      },
      yaxis: {
        decimalsInFloat: 2,
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
    <Loader loaded={pythonFile && loadedNumpy}>
      <PageContainer alignContent="flex-start" {...props}>
        <Grid item xs={12}>
          <Grid container justifyContent="center">
            <Grid item xs={12} sm={8} md={6}>
              <Chart
                options={chartData.options}
                series={chartData.series}
                type="line"
                width="100%"
              />
            </Grid>
            <Grid item xs={8}>
              <GridContainer>
                <Button onClick={() => visualizeData()} variant="contained">
                  Load data
                </Button>
              </GridContainer>
            </Grid>
            <ClearBlock pb={10} />
            <Grid item xs={8}>
              <SpacedGridContainer spacing={4} justifyContent="center">
                <Grid item xs={6}>
                  <GridContainer>
                    <Grid item xs={12}>
                      <Typography variant="h6" color="initial" align="center">
                        Theta amplitude
                      </Typography>
                    </Grid>
                    <Grid item xs={12}>
                      <Slider
                        //   defaultValue={0.2}
                        value={slidersNamespace.tAmp}
                        step={0.1}
                        min={sliderConfigs.minAmp}
                        max={sliderConfigs.maxAmp}
                        valueLabelDisplay="auto"
                        onChange={(e, v) => sliderCB(v, 'theta')}
                      />
                    </Grid>
                  </GridContainer>
                </Grid>
                <Grid item xs={6}>
                  <GridContainer>
                    <Grid item xs={12}>
                      <Typography variant="h6" color="initial" align="center">
                        Beta amplitude
                      </Typography>
                    </Grid>
                    <Grid item xs={12}>
                      <Slider
                        //   defaultValue={0.2}
                        value={slidersNamespace.bAmp}
                        step={0.1}
                        min={sliderConfigs.minAmp}
                        max={sliderConfigs.maxAmp}
                        valueLabelDisplay="auto"
                        onChange={(e, v) => sliderCB(v, 'beta')}
                      />
                    </Grid>
                  </GridContainer>
                </Grid>
              </SpacedGridContainer>
            </Grid>
          </Grid>
        </Grid>
      </PageContainer>
    </Loader>
  );
})`
  margin: 0 auto;
`;

export default IndexPage;
