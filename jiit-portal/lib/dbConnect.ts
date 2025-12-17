import mongoose from "mongoose";

type ConnectionObject = {
    isConnected?: number;
};

const connection: ConnectionObject = {};

async function dbConnect(): Promise<void> {
    if (connection.isConnected) {
        console.log("Using existing database connection");
        return;
    }
    try {
        if (!process.env.MONGODB_URI) {
            throw new Error("Please define the MONGODB_URI environment variable inside .env.local");
        }
        const db = await mongoose.connect(process.env.MONGODB_URI, {});
        connection.isConnected = db.connections[0].readyState;
        console.log("New database connection established");
    } catch (error) {
        console.log("Database connection failed", error);
        process.exit(1);
    }
}

export default dbConnect;
