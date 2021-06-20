import React from 'react'
import { Box, Text, Heading } from 'rebass/styled-components'


export default class ModelComponent extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            items: []
        }
    }
    fetchModels() {
        if (this.props.name) {
            fetch(`${process.env.REACT_APP_API_BASE}/model/find?name=${this.props.name} `, {
                referrerPolicy: 'origin'
            })
                .then(res => {
                    if (res.ok) {
                        return res.json()
                    } else {
                        throw Error("No such model found")
                    }
                }
                )
                .then(
                    (result) => {
                        this.setState({
                            isLoaded: true,
                            items: result
                        });
                    },
                    (error) => {
                        this.setState({
                            isLoaded: false,
                            error
                        });
                    }
                )
        }
    }

    componentDidMount() {
        this.fetchModels()
    }

    componentDidUpdate(prevProps) {
        if (prevProps.name !== this.props.name) {
            this.fetchModels();
        }
    }

    render() {
        const { error, isLoaded, items } = this.state;
        if (error) {
            return <div> Error: {error.message}</div>;
        } else {
            return (
                <Box >
                    <Heading bg='blue' color='white' fontSize={[3, 4, 5]}>SELECTED : {this.props.name}</Heading>
                    {!items && <Text>Nothing to show</Text>}
                    {items.map(item => (
                        <Box
                            width={[1, 1, 1 / 2]}
                            key={item.version} width={1}
                            p={3}>
                            <Heading
                                color='secondary'
                                fontStyle="initial"
                                fontSize={[5, 6, 7]}>
                                {item.version}
                            </Heading>
                            {item.is_active &&
                                <Text
                                    fontSize={[3, 4, 5]}
                                    fontWeight='bold'
                                    color='action'>
                                    active
                                </Text>
                            }
                            <Text
                                fontSize={[3, 4, 5]}
                                fontWeight='bold'
                                color='secondary'>
                                Artifacts: {item.artifact_path}
                            </Text>
                            <Text
                                fontSize={[3, 4, 5]}
                                fontWeight='bold'
                                color='secondary'>
                                Go Live on: {item.go_live_on}
                            </Text>

                        </Box>
                    ))}
                    <Heading bg='blue' color='white' fontSize={[3, 4, 5]}>SELECTED : {this.props.name}</Heading>
                </Box>
            );
        }
    }
}