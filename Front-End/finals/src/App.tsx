import React from "react";
import BasicTextFields from "./components/BasicTextField";
import { Box } from "@mui/material";
function App() {
  return (
    <Box
      sx={{
        backgroundImage: `url(https://logincdn.msauth.net/shared/1.0/content/images/appbackgrounds/49_6ffe0a92d779c878835b40171ffc2e13.jpg)`,
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
        backgroundPosition: "center center",
        height: "150vh",
      }}>
      <BasicTextFields />
    </Box>
  );
}

export default App;
