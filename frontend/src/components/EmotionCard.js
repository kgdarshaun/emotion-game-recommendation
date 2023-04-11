import React from 'react'

import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';

function EmoitionCard(props) {
	const { emotion } = props

	return (
		<Card 
			sx={{ 
				minWidth: 275,
				marginTop: '35%',
				display: 'flex',
				flexDirection: 'column',
				alignItems: 'center',
			}}>
			<CardContent>
				<Button 
					fullWidth 
					variant="text"
					onClick={() => {navigator.clipboard.writeText(emotion)}}
				>
					detected emotion : {emotion}
				</Button>
			</CardContent>
		</Card>
	);
}

export default EmoitionCard;