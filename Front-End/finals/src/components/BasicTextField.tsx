import * as React from "react";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import { Button, Container, Paper, Stack, Typography } from "@mui/material";

export default function BasicTextFields() {
  return (
    <Container
      sx={{
        display: "flex",
        justifyContent: "center",
        minWidth: "60%",
      }}>
      <Stack>
        <Typography variant="h6" marginTop={"15px"}>
          {"基于LR(1)的PL0文法代码分析器"}
        </Typography>
        <Typography variant="caption" marginBottom={"15px"}>
          {"作者：蔡俊志、涂江得、李伟佳"}
        </Typography>

        <TextField
          id="filled-multiline-flexible"
          label="输入PL0 代码"
          multiline
          minRows={10}
          maxRows={20}
          variant="filled"
        />
        <Paper sx={{ minWidth: "50%", marginTop: "15px" }}>
          <Box margin={"7px"}>27:6 token recognition error at: ':d' </Box>
          <Box margin={"7px"}>27:8 mismatched input '=' expecting ':=' </Box>
        </Paper>

        <Stack direction={"row"} margin={"10px"}>
          <Button variant="contained">分析</Button>
          <Button variant="outlined" sx={{ marginX: "5px" }}>
            生成并下载分析表
          </Button>
        </Stack>
      </Stack>
    </Container>
  );
}
