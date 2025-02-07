import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import "./App.css";
import { HomePage } from "./routes/home";
import { ThemeProvider } from "./components/theme/theme-provider";

function App() {
	return (
		<ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
			<div className="bg-background absolute left-0 top-0 h-screen w-screen flex flex-col">
				<Router>
					<Routes>
						<Route path="/" element={<HomePage />} />
					</Routes>
				</Router>
			</div>
		</ThemeProvider>
	);
}

export default App;
