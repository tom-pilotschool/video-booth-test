import { useEffect, useRef } from "react";
import axios from "axios";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
export const HomePage = () => {
	const videoRef = useRef<HTMLVideoElement>(null);
	const { toast } = useToast();

	const recordVideo = async () => {
		try {
			const { data } = await axios.post(
				"http://127.0.0.1:5000/start_recording"
			);
			console.log(data);
			toast({
				title: "Video recording started",
				description: "Please wait for the video to finish recording",
			});
		} catch (error) {
			console.error("Error recording video", error);
			toast({
				title: "Error recording video",
				description: "Please try again",
				variant: "destructive",
			});
		}
	};

	// useEffect(() => {
	// 	const videoElement = videoRef.current; // Store the ref in a variable

	// 	// Function to start the camera
	// 	const startCamera = async () => {
	// 		try {
	// 			// Request the video stream (no audio in this example)
	// 			const stream = await navigator.mediaDevices.getUserMedia({
	// 				video: true,
	// 				audio: false,
	// 			});
	// 			// If the video element is available, attach the stream to it
	// 			if (videoElement) {
	// 				videoElement.srcObject = stream;
	// 			}
	// 		} catch (error) {
	// 			console.error("Error accessing the camera", error);
	// 		}
	// 	};

	// 	startCamera();

	// 	// Cleanup: stop all media tracks when the component unmounts
	// 	return () => {
	// 		if (videoElement && videoElement.srcObject instanceof MediaStream) {
	// 			const tracks = videoElement.srcObject.getTracks();
	// 			tracks.forEach((track) => track.stop());
	// 		}
	// 	};
	// }, []);

	return (
		<div>
			<h2>Camera Feed</h2>
			{/* <video
				ref={videoRef}
				autoPlay
				playsInline
				style={{
					width: "100%",
					maxWidth: "640px",
					border: "1px solid #ccc",
				}}
			/> */}
			<Button onClick={recordVideo}>Record Video</Button>
		</div>
	);
};
