"use client";

import { useSession } from "next-auth/react";
import { useEffect } from "react";

export function SessionSync() {
	const { data: session } = useSession();

	useEffect(() => {
		if (session?.user && (session.user as { id: string }).id) {
			const userId = (session.user as { id: string }).id;
			// If localStorage is missing or different, update it
			if (localStorage.getItem("user_id") !== userId) {
				localStorage.setItem("user_id", userId);
				console.log("SessionSync: Updated user_id in localStorage");
			}
		}
	}, [session]);

	return null;
}
