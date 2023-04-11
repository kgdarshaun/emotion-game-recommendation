import React from 'react'

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Link from '@mui/material/Link';
import LaunchIcon from '@mui/icons-material/Launch';

function TableGames(props) {
	const { tableData } = props;
  
	return (
		<TableContainer>
      <Table sx={{ minWidth: 450 }}>
        <TableHead>
          <TableRow>
            <TableCell sx={{ color: 'text.secondary' }} >Steam ID</TableCell>
            <TableCell sx={{ color: 'text.secondary' }} >Title</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {tableData.map((row) => (
            <TableRow key={row.product_id}>
              <TableCell>
                <Link href={`https://store.steampowered.com/app/${row.product_id}`} target="_blank" underline="hover">
                  {row.product_id}
                  <LaunchIcon color="primary"  sx={{ marginLeft: 0.5, fontSize: 12 }}/>
                </Link>
              </TableCell>
              <TableCell>{row.title}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
	);
}

export default TableGames;