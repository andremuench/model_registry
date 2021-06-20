import './App.css';
import ModelComponent from './ModelComponent';
import React from 'react';
import { ThemeProvider } from 'styled-components'
import { Flex, Box, Button, Heading, Text, Link } from 'rebass/styled-components'
import preset from '@rebass/preset'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faRobot } from '@fortawesome/free-solid-svg-icons'



function ModelIdItem({ name, clickHandler }) {
  return (
    <Box as="form" onSubmit={e => e.preventDefault()}>
      <FontAwesomeIcon icon={faRobot} />
      <Link
        variant='nav'
        href='#'
        fontSize={[3, 4, 5]}
        onClick={clickHandler}>
        {name}
      </Link>
    </Box>
  );
}

function ModelList({ models, clickHandler }) {
  const listItems = models.map((model) =>
    <ModelIdItem name={model} clickHandler={(e) => clickHandler(model, e)} />
  );
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        minHeight: '100vh'
      }}>
      <Box
        sx={{
          p: 3
        }}>
        <Heading variant='display'>Models</Heading>
      </Box>
      <Box
        sx={{
          display: 'grid',
          gridGap: 3,
          gridTemplateColumns: 'repeat(auto-fit, minmax(256px, 1fr))'
        }}>
        {listItems}
      </Box>
    </Box>
  );
}


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      isLoaded: false,
      selectedModel: null,
      models: [],
      error: null,
    }
  }

  changeModel = (model, e) => {
    this.setState({ selectedModel: model })
  }

  fetchModelIds() {
    fetch(`${process.env.REACT_APP_API_BASE}/model/ids`)
      .then(res => {
        if (res.ok) {
          return res.json()
        } else {
          throw Error(res.statusText)
        }
      })
      .then(
        (result) => {
          this.setState({
            models: result.map(x => x.model_id),
            isLoaded: true
          })
        },
        (error) => {
          this.setState({
            isLoaded: false,
            error
          })
        }
      )
  }

  componentDidMount() {
    this.fetchModelIds()
  }

  render() {
    return (
      <ThemeProvider theme={preset}>
        <div className="App">
          <Flex
            px={2}
            color='white'
            bg='black'
            alignItems='center'>
            <Text p={2} fontWeight='bold'>Model Registry</Text>
            <Box mx='auto' />
            <Text p={2} fontWeight='bold'>{process.env.REACT_APP_SPONSOR}</Text>
          </Flex>
          <main>
            <Flex
              sx={{
                flexWrap: 'wrap'
              }}>
              <Box
                sx={{
                  p: 3,
                  flexGrow: 1,
                  flexBasis: 256
                }}>
                <ModelList models={this.state.models} clickHandler={this.changeModel} />
              </Box>
              <Box
                sx={{
                  p: 3,
                  flexGrow: 99999,
                  flexBasis: 0,
                  minWidth: 320
                }}>
                <ModelComponent name={this.state.selectedModel} />
              </Box>
            </Flex>

          </main>
        </div>
      </ThemeProvider>

    );
  }
}
export default App;
