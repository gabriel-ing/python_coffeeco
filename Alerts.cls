Class coffeeco.Alerts
{

ClassMethod OutOfStockAlert(pId As %Integer, pName As %Name) As %String [ Language = python ]
{
        return f"Sent internal out of stock alert for product {pName}"
}

ClassMethod LowStockAlert(pId As %Integer, pName As %Name) As %String [ Language = python ]
{
        return f"Sent internal out of stock alert for product {pName}"
}

}
