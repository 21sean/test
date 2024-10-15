import streamlit as st
import streamlit.components.v1 as components

st.title('Weather Widget')

# Embed your weather widget here
widget_code = """
<a class="weatherwidget-io" href="https://forecast7.com/en/40d71n74d01/new-york/" data-label_1="NEW YORK" data-label_2="WEATHER" data-days="3" data-theme="pure" >NEW YORK WEATHER</a>
<script>
!function(d,s,id){
  var js,fjs=d.getElementsByTagName(s)[0];
  if(!d.getElementById(id)){
    js=d.createElement(s);js.id=id;js.src='https://weatherwidget.io/js/widget.min.js';
    fjs.parentNode.insertBefore(js,fjs);
  }
}(document,'script','weatherwidget-io-js');
</script>
"""

components.html(widget_code, height=300)

