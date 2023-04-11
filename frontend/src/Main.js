import React, { useRef, useState } from "react";

import axios from 'axios';

import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import LoadingButton from '@mui/lab/LoadingButton';
import MuiAlert from '@mui/material/Alert';
import Snackbar from '@mui/material/Snackbar';

import IdentifierInput from "./components/IdentifierInput";
import BeforeCapture from "./components/BeforeCapture";
import AfterCapture from "./components/AfterCapture";
import EmoitionCard from "./components/EmotionCard";
import TableGames from './components/TableGames'

function Main() {
  const webcamRef = useRef(null);
  const [isUser, setIsUser] = useState(true);
  const [input, setInput] = useState('');
  const [photo, setPhoto] = useState(null);
  const [emotion, setEmotion] = useState('');
  const [tableData, setTableData] = useState([]);
  const [empty, setEmpty] = useState(true);
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(false)

  const [snackbar, setSnackbar] = useState({ message: '', severity: 'info', open: false});

  const identifierInputProps = { isUser, input, photo, error, loading, setIsUser, setEmpty, setInput, setEmotion, setTableData, setError }
  const beforeCaptureProps = { input, webcamRef, setPhoto, setEmpty }
  const afterCaptureProps = { photo, loading, setPhoto, setEmpty, setEmotion, setTableData }


  const handleCloseSnackbar = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setSnackbar({ ...snackbar, open: false });
  };
  
  const get_recommendations = () => {
    setLoading(true)
    console.log(photo)
    axios.post("https://recommendation-s4zjzkisqq-uw.a.run.app/recommend", {
      is_user: isUser,
      id: input,
      image: photo
    })
    .then(response => {
      if(response.data.games.length === 0){
        setSnackbar({ message: `The ${isUser ? "user" : "steam"} ID might not exist in database`, severity: 'warning' , open: true});
      }
      setTableData(response.data.games);
      setEmotion(response.data.emotion)
      setLoading(false)
    })
    .catch(error => {
      setSnackbar({ message: 'Error!', severity: 'error' , open: true });
      console.error(error);
      setLoading(false)
    });
  }
  
  
  return (
    <Container component="main">
      <Grid container spacing={2}>
        <Grid item xs={6}>
          <Card 
            sx={{ 
              minWidth: 275,
              marginTop: '10%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}>
            <CardContent>
              <IdentifierInput identifierInputProps={identifierInputProps}/>
              { photo === null ? (
                <BeforeCapture beforeCaptureProps={beforeCaptureProps}/>
              ) : (
                <AfterCapture afterCaptureProps={afterCaptureProps}/>
              )}
              <LoadingButton
                fullWidth
                loading={loading}
                variant="contained"
                sx={{ marginTop: 1, marginBottom: 0.5 }}
                onClick={get_recommendations}
                disabled={empty}
              >
                get recommendations
              </LoadingButton>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6}>
          <EmoitionCard  emotion={emotion}/>
          <Card
            sx={{ 
              minWidth: 275,
              marginTop: 2,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}>
            <CardContent>
              <TableGames tableData={tableData} />
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      <Snackbar open={snackbar.open} autoHideDuration={5000} onClose={handleCloseSnackbar} anchorOrigin={{ vertical: 'top', horizontal: 'center' }}>
        <MuiAlert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </MuiAlert>
      </Snackbar>
    </Container>
  );
}

export default Main;