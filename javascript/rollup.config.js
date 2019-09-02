import typescript from 'rollup-plugin-typescript';

export default {
    input: './main.ts',
    output: {
        file: 'index.js',
        format: 'umd',
        name: 'MicroSocket'
    },
    plugins: [
        typescript()
    ]
}
