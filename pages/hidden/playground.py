import streamlit as st
import iris 


st.write("hello world")

connection = iris.connect("localhost", 1972, "USER", "SuperUser", "SYS")
irispy = iris.createIRIS(connection)

val = irispy.classMethod("coffeeco.Inventory", "ExtentFunc")


for row in val:  # Assuming result is iterable
    print(row)
