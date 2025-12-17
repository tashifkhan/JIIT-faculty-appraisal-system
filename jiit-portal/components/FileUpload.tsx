"use client";

import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Upload, X, FileIcon } from "lucide-react";
import { toast } from "sonner";

interface FileUploadProps {
	onFileSelect: (base64: string | null, fileName: string | null) => void;
	maxSizeInMB?: number;
	acceptedTypes?: string;
	currentFile?: string | null; // For displaying existing file state if needed
}

export function FileUpload({
	onFileSelect,
	maxSizeInMB = 0.5, // Default 500KB
	acceptedTypes = "image/*,application/pdf",
}: FileUploadProps) {
	const [fileName, setFileName] = useState<string | null>(null);
	const [preview, setPreview] = useState<string | null>(null);
	const fileInputRef = useRef<HTMLInputElement>(null);

	const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		const file = e.target.files?.[0];
		if (!file) return;

		// Validation
		if (file.size > maxSizeInMB * 1024 * 1024) {
			toast.error(`File size must be less than ${maxSizeInMB}MB`);
			if (fileInputRef.current) fileInputRef.current.value = "";
			return;
		}

		// Read file
		const reader = new FileReader();
		reader.onloadend = () => {
			const base64String = reader.result as string;
			setFileName(file.name);
			setPreview(base64String);
			onFileSelect(base64String, file.name || "uploaded_file");
		};
		reader.readAsDataURL(file);
	};

	const handleRemove = () => {
		setFileName(null);
		setPreview(null);
		onFileSelect(null, null);
		if (fileInputRef.current) fileInputRef.current.value = "";
	};

	return (
		<div className="flex items-center gap-3">
			<input
				type="file"
				ref={fileInputRef}
				className="hidden"
				accept={acceptedTypes}
				onChange={handleFileChange}
			/>

			{!fileName ? (
				<Button
					type="button"
					variant="secondary"
					size="sm"
					onClick={() => fileInputRef.current?.click()}
				>
					<Upload className="h-4 w-4 mr-2" />
					Upload Proof
				</Button>
			) : (
				<div className="flex items-center gap-2 bg-muted px-3 py-1.5 rounded-md text-sm">
					<FileIcon className="h-4 w-4 text-primary" />
					<span className="max-w-[150px] truncate" title={fileName}>
						{fileName}
					</span>
					<button
						type="button"
						onClick={handleRemove}
						className="text-muted-foreground hover:text-destructive transition-colors"
					>
						<X className="h-4 w-4" />
					</button>
				</div>
			)}
			{fileName && preview?.startsWith("data:image") && (
				<div className="relative group">
					{/* Tiny preview on hover could go here, or just keep it simple */}
				</div>
			)}
		</div>
	);
}
