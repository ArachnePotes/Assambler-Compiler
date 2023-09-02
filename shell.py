import basic

text = ''' <tfc>
            <autor>hola</autor>
            <fecha_nac>12/12/2020</fecha_nac>
            <titulo_tfc></titulo_tfc>
            <tutor></tutor>
            <nota>3.0</nota>
        </tfc> '''
result , error = basic.run('<stdin>',text)
if error: print(error.as_string())
else: print(result)

