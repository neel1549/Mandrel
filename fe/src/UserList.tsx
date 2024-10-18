import { useEffect, useState } from "react";
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import io from "socket.io-client";

// Define the User type
interface User {
    _id: string;
    name: string;
    email: string;
}

const UserList = () => {
    // Set initial state with the type User[] | undefined, and default to an empty array
    const [users, setUsers] = useState<User[]>([]);

    useEffect(() => {
        // Connect to the WebSocket server
        const socket = io("https://mandrel-test-f0944079ae57.herokuapp.com/"     // When running in Docker Compose
        );
        // Receive the initial list of users
        socket.on("initial_slack_users", (initialUsers) => {
            setUsers(initialUsers);
        });

        socket.on("update_slack_users", (initialUsers) => {
            setUsers(initialUsers);
        });

        // Clean up the connection when the component unmounts
        return () => {
            socket.disconnect(); // Ensure WebSocket connection is cleaned up properly
        };
    }, []);
    return (
        <div>
            <h4>Mandrel Slack Workspace</h4>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead sx={{ fontWeight: 'bold', backgroundColor: '#f0f0f0' }}>
                        <TableRow >
                            <TableCell>Id</TableCell>
                            <TableCell>Name</TableCell>
                            <TableCell>Email</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {users.map((row, index) => (
                            <TableRow
                                key={index}
                            >
                                <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f0f0f0' }} component="th" scope="row">
                                    {index}
                                </TableCell>
                                <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f0f0f0' }} component="th" scope="row">
                                    {row.name}
                                </TableCell>
                                <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f0f0f0' }} >{row.email}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    )

}


export default UserList;
